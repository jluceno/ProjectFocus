Module.register("timeular_test_module", {
	getScripts: function () {
		return ["moment.js"];
	},

	start: function () {
		var self = this;
		this.timeular_template_data;

		// Schedule update timer.
		setInterval(function () {
			self.updateDom();
			template_data = fetch('http://127.0.0.1:5000/timeular')
			.then(function (response) {
				return response.json();
			})
			.then(function (time_resp) {
				self.timeular_template_data = time_resp
			});
		}, 3000);
	},

	getTemplate: function () {
		return "timeular_test_module_template.njk";
	},

	getTemplateData: function () {
		return this.timeular_template_data;
	}
});
