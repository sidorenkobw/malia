define(["view", "model/user", "firebase-proxy"], function (View, User, FirebaseProxy) {
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

    return AuthView;
});
