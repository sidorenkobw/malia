class FirebaseProxy extends EventEmitter {
    constructor(cfg) {
        super();
        this.cfg = cfg || {};
        this.authContainerSelector = null;
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

        var uiConfig = {
            signInOptions: [
                firebase.auth.GoogleAuthProvider.PROVIDER_ID,
            ],
            tosUrl: '<your-tos-url>', // TODO create terms of service URL
            signInFlow: 'popup',
            callbacks: {
                signInSuccess: function(user, credential, redirectUrl) {
                    handleSignedInUser(user);
                    // Do not redirect.
                    return false;
                }
            }
        };

        var ui = new firebaseui.auth.AuthUI(firebase.auth()),
            self = this;

        ui.start(this.authContainerSelector, uiConfig);
        firebase.auth().onAuthStateChanged(function(user) {
            if (user) {
                self.emit("sign-in", user);
            } else {
                self.emit("sign-out", user);
            }
        }, function(error) {
            self.emit("error", error);
        });
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
