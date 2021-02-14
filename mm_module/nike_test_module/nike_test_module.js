Module.register("nike_test_module", {
	getScripts: function () {
		return ["moment.js"];
	},

	start: function () {
		var self = this;
		this.nike_template_data;

		// Schedule update timer.
		setInterval(function () {
			self.updateDom();
			template_data = fetch('http://127.0.0.1:5000/nike')
			.then(function (response) {
				return response.json();
			})
			.then(function (nike_resp) {
				self.nike_template_data = nike_resp
			});
		}, 3000);
	},

	getTemplate: function () {
		return "nike_test_module_template.njk";
	},

	getTemplateData: function () {
		return this.nike_template_data;
	}
});
