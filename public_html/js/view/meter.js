define(function () {
    class Meter {
        constructor(elem, stream) {
            this.elem = elem;
            let ctx = new AudioContext();
            this.analyser = ctx.createAnalyser();
            let microphone = ctx.createMediaStreamSource(stream);
            microphone.connect(this.analyser);

            this.analyser.fftSize = 128;
            this.dataArray = new Uint8Array(this.analyser.fftSize);

            this.update();
        }

        update() {
            this.analyser.getByteTimeDomainData(this.dataArray);
            let maxLevel = 0;
            this.dataArray.forEach((e) => {
                let mag = Math.abs(e - 128);
                if (mag > maxLevel) {
                    maxLevel = mag;
                }
            });
            let bars = Math.max(0, Math.round(Math.log(maxLevel)));
            this.elem.innerHTML = "&#x1f431;".repeat(bars);
            requestAnimationFrame(function() {
                setTimeout(this.update.bind(this), 100);
            }.bind(this));
        }
    }

    return Meter;
});
