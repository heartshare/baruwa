dojo.provide("dojox.charting.plot2d.Bars");

dojo.require("dojox.charting.plot2d.common");
dojo.require("dojox.charting.plot2d.Base");
dojo.require("dojox.gfx.fx");

dojo.require("dojox.lang.utils");
dojo.require("dojox.lang.functional");
dojo.require("dojox.lang.functional.reversed");

(function(){
	var df = dojox.lang.functional, du = dojox.lang.utils,
		dc = dojox.charting.plot2d.common,
		purgeGroup = df.lambda("item.purgeGroup()");

	dojo.declare("dojox.charting.plot2d.Bars", dojox.charting.plot2d.Base, {
		defaultParams: {
			hAxis: "x",		// use a horizontal axis named "x"
			vAxis: "y",		// use a vertical axis named "y"
			gap:	0,		// gap between columns in pixels
			shadows: null,	// draw shadows
			animate: null   // animate bars into place
		},
		optionalParams: {
			minBarSize: 1,	// minimal bar size in pixels
			maxBarSize: 1	// maximal bar size in pixels
		},

		constructor: function(chart, kwArgs){
			this.opt = dojo.clone(this.defaultParams);
			du.updateWithObject(this.opt, kwArgs);
			du.updateWithPattern(this.opt, kwArgs, this.optionalParams);
			this.series = [];
			this.hAxis = this.opt.hAxis;
			this.vAxis = this.opt.vAxis;
			this.animate = this.opt.animate;
		},

		calculateAxes: function(dim){
			var stats = dc.collectSimpleStats(this.series), t;
			stats.hmin -= 0.5;
			stats.hmax += 0.5;
			t = stats.hmin, stats.hmin = stats.vmin, stats.vmin = t;
			t = stats.hmax, stats.hmax = stats.vmax, stats.vmax = t;
			this._calc(dim, stats);
			return this;
		},
		render: function(dim, offsets){
			this.dirty = this.isDirty();
			if(this.dirty){
				dojo.forEach(this.series, purgeGroup);
				this.cleanGroup();
				var s = this.group;
				df.forEachRev(this.series, function(item){ item.cleanGroup(s); });
			}
			var t = this.chart.theme, color, stroke, fill, f, gap, height,
				ht = this._hScaler.scaler.getTransformerFromModel(this._hScaler),
				vt = this._vScaler.scaler.getTransformerFromModel(this._vScaler),
				baseline = Math.max(0, this._hScaler.bounds.lower),
				baselineWidth = ht(baseline),
				events = this.events();
			f = dc.calculateBarSize(this._vScaler.bounds.scale, this.opt);
			gap = f.gap;
			height = f.size;
			this.resetEvents();
			for(var i = this.series.length - 1; i >= 0; --i){
				var run = this.series[i];
				if(!this.dirty && !run.dirty){ continue; }
				run.cleanGroup();
				var s = run.group;
				if(!run.fill || !run.stroke){
					// need autogenerated color
					color = run.dyn.color = new dojo.Color(t.next("color"));
				}
				stroke = run.stroke ? run.stroke : dc.augmentStroke(t.series.stroke, color);
				fill = run.fill ? run.fill : dc.augmentFill(t.series.fill, color);
				for(var j = 0; j < run.data.length; ++j){
					var value = run.data[j],
						v = typeof value == "number" ? value : value.y,
						hv = ht(v),
						width = hv - baselineWidth,
						w = Math.abs(width),
						specialColor  = color,
						specialFill   = fill,
						specialStroke = stroke;
					if(typeof value != "number"){
						if(value.color){
							specialColor = new dojo.Color(value.color);
						}
						if("fill" in value){
							specialFill = value.fill;
						}else if(value.color){
							specialFill = dc.augmentFill(t.series.fill, specialColor);
						}
						if("stroke" in value){
							specialStroke = value.stroke;
						}else if(value.color){
							specialStroke = dc.augmentStroke(t.series.stroke, specialColor);
						}
					}
					if(w >= 1 && height >= 1){
						var shape = s.createRect({
							x: offsets.l + (v < baseline ? hv : baselineWidth),
							y: dim.height - offsets.b - vt(j + 1.5) + gap,
							width: w, height: height
						}).setFill(specialFill).setStroke(specialStroke);
						run.dyn.fill   = shape.getFill();
						run.dyn.stroke = shape.getStroke();
						if(events){
							var o = {
								element: "bar",
								index:   j,
								run:     run,
								plot:    this,
								hAxis:   this.hAxis || null,
								vAxis:   this.vAxis || null,
								shape:   shape,
								x:       v,
								y:       j + 1.5
							};
							this._connectEvents(shape, o);
						}
						if(this.animate){
							this._animateBar(shape, offsets.l + baselineWidth, -w);
						}
					}
				}
				run.dirty = false;
			}
			this.dirty = false;
			return this;
		},
		_animateBar: function(shape, hoffset, hsize){
			dojox.gfx.fx.animateTransform(dojo.delegate({
				shape: shape,
				duration: 1200,
				transform: [
					{name: "translate", start: [hoffset - (hoffset/hsize), 0], end: [0, 0]},
					{name: "scale", start: [1/hsize, 1], end: [1, 1]},
					{name: "original"}
				]
			}, this.animate)).play();
		}
	});
})();