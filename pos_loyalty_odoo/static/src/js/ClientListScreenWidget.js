odoo.define('pos_loyalty_odoo.ClientListScreenWidget', function(require) {
	"use strict";

	const ClientListScreen = require('point_of_sale.ClientListScreen');
	const { debounce } = owl.utils;
	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');
	const { useListener } = require('web.custom_hooks');


	const ClientListScreenWidget = (ClientListScreen) =>
		class extends ClientListScreen {
			constructor() {
				super(...arguments);
				var self = this;
				setInterval(function(){
					self.searchClient();
				}, 5000);
				this.searchClient()
			}
	};

	Registries.Component.extend(ClientListScreen, ClientListScreenWidget);

	return ClientListScreen;
});
