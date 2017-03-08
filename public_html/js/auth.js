class FirebaseProxy extends EventEmitter {
    constructor(cfg) {
        super();
        this.cfg = cfg || {};
        this.ui = null;
        this.authContainerSelector = null;
        this.uiConfig = {
            signInFlow: "popup",
            signInOptions: [
                firebase.auth.GoogleAuthProvider.PROVIDER_ID,
            ],
            tosUrl: "<your-tos-url>", // TODO create terms of service URL
            callbacks: {
                signInSuccess: (function(user, credential, redirectUrl) {
                    this.onSingIn(user);
                    // Do not redirect.
                    return false;
                }).bind(this)
            }
        };
    }
    
    setAuthContainerSelector(selector)
    {
        this.authContainerSelector = selector;
        return this;
    }
    
    init() {
        if (!firebase) {
            throw new Error("missing firebase.js");
        }
        
        firebase.initializeApp(this.cfg);

        this.ui = new firebaseui.auth.AuthUI(firebase.auth());
        var currentUid = null;
        
        firebase.auth().onAuthStateChanged((function(user) {
            // The observer is also triggered when the user's token has expired and is
            // automatically refreshed. In that case, the user hasn't changed so we should
            // not update the UI.
            if (user && user.uid == currentUid) {
                return;
            }
            
            // TODO render loading
            user ? this.onSingIn(user) : this.onSignOut();
        }).bind(this), (function(error) {
            this.emit("error", error);
        }).bind(this));
    }
    
    onSingIn(user) {
        this.emit("sign-in", user);
    }
    
    onSignOut() {
        this.emit("sign-out");
        this.ui.start(this.authContainerSelector, this.uiConfig);
    }
    
    signOut() {
        firebase.auth().signOut();
    }
    
    upload(blob, path) {
        var storage = firebase.storage();
        var storageRef = storage.ref();
        var ref = storageRef.child(path);
        return ref.put(blob);
    }
}

class AuthView extends View {
    constructor(malia) {
        super();
        
        this.cfg = malia.cfg || {};
        
        this.firebaseProxy = new FirebaseProxy(this.cfg.auth.firebase);
        this.firebaseProxy
            .setAuthContainerSelector("#firebaseui-auth-container")
            .on("sign-in", this.onSignIn.bind(this))
            .on("sign-out", this.onSignOut.bind(this))
            .on("error", this.onError.bind(this));
        
        this.firebaseProxy.init();
        
        this.$authAlert = $(".alert.auth");
        this.$btnSignout = $(".btnSignout")
            .on("click", this.onClickSignOut.bind(this));
    }
    
    onClickSignOut(e) {
        e.preventDefault();
        this.firebaseProxy.signOut();
    }
    
    onSignIn(user) {
        this.emit("sign-in");
        this.debug("Signed in");
        this.debug({
            displayName: user.displayName,
            email: user.email,
            emailVerified: user.emailVerified,
            photoURL: user.photoURL,
            uid: user.uid,
            // accessToken: accessToken,
            providerData: user.providerData            
        });
        
        this.$authAlert.addClass("hidden");
        this.$btnSignout.removeClass("hidden");
    }
    
    onSignOut(user) {
        this.emit("sign-out");
        
        this.$authAlert.removeClass("hidden");
        this.$btnSignout.addClass("hidden");
        
        this.debug("Signed out");
    }
    
    onError(e) {
        this.emit("error", e);
        this.debug(e);
        this.showNotification("danger", "Authentication error");
    }
    
    getProxy() {
        return this.firebaseProxy;
    }
}
