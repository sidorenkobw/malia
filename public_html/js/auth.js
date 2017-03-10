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

class User extends EventEmitter {
    constructor(data, role) {
        super();
        
        if (!data) {
            role = null;
        } else {
            if (!("uid" in data)) {
                throw new Error("Invalid user");
            }
            
            this.data = data || {};
            
        }
        
        this.setRole(role || "guest");
    }
    
    setRole(role) {
        this.role = role;
    }
    
    getRole() {
        return this.role;
    }
    
    get(attr) {
        return this.data[attr] || null;
    }
    
    getId() {
        if (this.role == "guest") {
            throw new Error("Guests don't have ids");
        }
        
        if ("uid" in this.data) {
            return this.data.uid;
        } else {
            throw new Error("No user id");
        }
    }
}

class AuthView extends View {
    constructor(malia) {
        super();
        
        this.cfg = malia.cfg || {};
        
        if (malia.debugLog) {
            this.setDebugLog(malia.debugLog);
        }
        
        this.initGuest();
        
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
    
    initGuest() {
        this.user = new User();
    }
    
    getUser() {
        return this.user;
    }
    
    getProxy() {
        return this.firebaseProxy;
    }
    
    onClickSignOut(e) {
        e.preventDefault();
        this.firebaseProxy.signOut();
    }
    
    onSignIn(user) {
        this.debug("Signed in", "log", "Auth");
        this.user = new User({
            displayName: user.displayName,
            email: user.email,
            emailVerified: user.emailVerified,
            photoURL: user.photoURL,
            uid: user.uid,
            // accessToken: accessToken,
            providerData: user.providerData            
        });
        this.user.setRole("authenticated");
        this.debug(this.user, "log", "Auth");
        
        this.$authAlert.addClass("hidden");
        this.$btnSignout.removeClass("hidden");
        
        this.emit("sign-in");
    }
    
    onSignOut(user) {
        this.initGuest();
        this.$authAlert.removeClass("hidden");
        this.$btnSignout.addClass("hidden");
        
        this.emit("sign-out");
        this.debug("Signed out", "log", "Auth");
    }
    
    onError(e) {
        this.emit("error", e);
        this.debug(e);
        this.showNotification("danger", "Authentication error");
    }
}
