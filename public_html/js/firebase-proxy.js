define(["event-emitter"], function (EventEmitter) {
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

    return FirebaseProxy;
});
