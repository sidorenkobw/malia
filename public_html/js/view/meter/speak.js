define(["view/meter"], function (MeterView) {
    class SpeakMeterView extends MeterView {
        constructor(elem) {
            super(elem);

            this.canvas = document.createElement("canvas");
            this.canvas.width = 900;
            this.canvas.height = 300;
            this.canvas.style.display = "block";
            this.canvas.style.margin = "0 auto";
            $(elem).append(this.canvas);
            this.ctx = this.canvas.getContext("2d");

            this.isActivated = false;
            this.threshold = 15;
            this.thresholdCount = 200;

            this.minCounter = 0;
        }

        update() {
            this.analyser.getByteTimeDomainData(this.dataArray);
            this.ctx.clearRect(0,0,this.canvas.width, this.canvas.height);

            var x = 0;
            this.ctx.beginPath();
            this.ctx.moveTo(x, Math.round(this.canvas.height/2));

            var maxLevel = 0;

            this.dataArray.forEach((e) => {
                var mag = Math.abs(e - 128),
                    oldIsActivated = this.isActivated;

                if (mag > this.threshold) {
                    this.isActivated = true;
                    this.minCounter = 0;
                } else {
                    this.minCounter++;
                }

                if (this.minCounter > this.thresholdCount) {
                    this.isActivated = false;
                }

                if (oldIsActivated && !this.isActivated) {
                    this.emit("word-stop");
                }

                if (!oldIsActivated && this.isActivated) {
                    this.emit("word-start");
                }

                x = x + 7;
                this.ctx.lineTo(x, this.canvas.height/2 - mag);

                if (mag > maxLevel) {
                    maxLevel = mag;
                }
            });

            this.ctx.stroke();

            requestAnimationFrame(function() {
                setTimeout(this.update.bind(this), 100);
            }.bind(this));
        }
    }

    return SpeakMeterView;
});
