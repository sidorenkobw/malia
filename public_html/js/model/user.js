define(["event-emitter"], function (EventEmitter) {
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

    return User;
});
