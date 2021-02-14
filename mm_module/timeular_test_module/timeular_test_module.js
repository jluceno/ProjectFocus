Module.register("timeular_test_module", {
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
				self.nike_template_data = {
					latest_calories : nike_resp.latest_calories,
					latest_miles : nike_resp.latest_miles,
					total_calories : nike_resp.total_calories,
					total_miles : nike_resp.total_miles
				};
			});
		}, 3000);
	},

	getTemplate: function () {
		return "test_module.njk";
	},

	getTemplateData: function () {
		return this.nike_template_data;
	}
});
