Module.register("testfocusmodule", {

	getScripts: function () {
		return ["moment.js"];
	},

	start: function () {
		var self = this;
		
		// Schedule update timer.
		setInterval(function () {
			self.updateDom();
		}, 3000);
	},

	getDom: function() {
		var wrapper = document.createElement("div");

		fetch('http://127.0.0.1:5000/update')
		.then(function (response) {
			return response.json();
		}).then(function (text) {
			wrapper.innerHTML = text.greeting;
		});

		console.log(wrapper);

		return wrapper;
	}
});
