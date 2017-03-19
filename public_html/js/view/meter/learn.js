define(["view/meter"], function (MeterView) {
    class LearnMeterView extends MeterView {
        constructor(elem) {
            super(elem);
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

    return LearnMeterView;
});
