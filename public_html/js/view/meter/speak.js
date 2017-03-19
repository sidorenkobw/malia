define(["view/meter"], function (MeterView) {
    class SpeakMeterView extends MeterView {
        constructor(elem) {
            super(elem);

            this.canvas = document.createElement("canvas");
            this.canvas.width = 700;
            this.canvas.height = 200;
            this.canvas.style.display = "block";
            this.canvas.style.margin = "0 auto";
            $(elem).append(this.canvas);
            this.ctx = this.canvas.getContext("2d");

            this.oldIsActivated = false;
            this.isActivated = false;
            this.thresholdSec = .2;

            this.minCounter = 0;

            this.prevAvg = 0;
            this.periodMs = 20;
            this.historyMs = 5000;
            this.history = [];
            this.histAboveThreshold = [];
            this.thresholdQuiet = 0;
            this.historicalPeak = 1;
        }

        start() {
            super.start();
            this.redraw();
        }

        redraw() {
            let w = this.canvas.width, h = this.canvas.height;
            this.ctx.clearRect(0, 0, w, h);

            let yFromMag = function(mag) {
                return (h - 5) * (1 - (mag / this.historicalPeak));
            }.bind(this);

            this.ctx.strokeStyle = '#ffaa00';
            this.ctx.beginPath();
            this.ctx.moveTo(0, yFromMag(this.thresholdQuiet));
            this.ctx.lineTo(w, yFromMag(this.thresholdQuiet));
            this.ctx.stroke();

            this.ctx.strokeStyle = '#000000';
            var x = 0;
            this.ctx.beginPath();
            this.ctx.moveTo(x, yFromMag(0));
            var dx = w / (this.historyMs / this.periodMs);
            this.history.forEach((mag) => {
                x = x + dx;
                this.ctx.lineTo(x, yFromMag(mag));
            });
            this.ctx.stroke();

            this.ctx.strokeStyle = '#aa0000';
            x = 0;
            this.histAboveThreshold.forEach((above) => {
                if (above) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(x, yFromMag(0));
                    this.ctx.lineTo(x, yFromMag(1));
                    this.ctx.stroke();
                }
                x = x + dx;
            });

            requestAnimationFrame(function() {
                setTimeout(this.redraw.bind(this), this.periodMs);
            }.bind(this));
        }

        update() {
            this.analyser.getByteTimeDomainData(this.dataArray);
            let avgLevel = 0;
            this.dataArray.forEach((e) => {
                let mag = Math.abs(e - 128) / 128;
                avgLevel += mag;
            });
            avgLevel /= this.dataArray.length;

            let smooth = .7;
            let smoothedAvg = smooth * this.prevAvg + (1 - smooth) * avgLevel;
            this.prevAvg = smoothedAvg;


            this.minPeak = .3;
            this.historicalPeak = Math.max(this.minPeak,
                                           Math.max.apply(null, this.history));

            let histLen = this.historyMs / this.periodMs;

            let v = this.history.slice();
            v.sort();
            let smoothQuiet = .8;
            let currentQuiet = v[Math.floor(histLen * .8)] * .5;
            if (!isNaN(currentQuiet)) {
                this.thresholdQuiet = (smoothQuiet * this.thresholdQuiet +
                                       (1 - smoothQuiet) * currentQuiet);
            }

            if (smoothedAvg > this.thresholdQuiet) {
                this.isActivated = true;
                this.minCounter = 0;
            } else {
                this.minCounter++;
            }


            if (this.minCounter > (this.thresholdSec * 1000) / this.periodMs) {
                this.isActivated = false;
            }

            if (this.oldIsActivated && !this.isActivated) {
                this.emit("word-stop");
            }

            if (!this.oldIsActivated && this.isActivated) {
                this.emit("word-start");
            }
            this.oldIsActivated = this.isActivated;


            this.history.push(smoothedAvg);
            this.histAboveThreshold.push(smoothedAvg > this.thresholdQuiet);

            if (this.history.length > histLen) {
                this.history.splice(0, 1);
                this.histAboveThreshold.splice(0, 1);
            }

            setTimeout(this.update.bind(this), this.periodMs);
        }
    }

    return SpeakMeterView;
});
