odoo.define('pos_salesperson.SalespersonButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class SalespersonButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        async onClick() {
            const selectionList = this.env.pos.users.map(user => ({
                id: user.id,
                label: user.name,
                item: user,
            }));

            const { confirmed, payload: selectedUser } = await this.showPopup(
                'SelectionPopup',
                {
                    title: this.env._t('Select Salesperson'),
                    list: selectionList,
                }
            );

            if (!confirmed) return false;

            if (confirmed) {
                var order = this.env.pos.get_order();
                var orderlines = order.get_orderlines();
                for(var i = 0; i < orderlines.length; i++){
                    if(orderlines[i] != undefined){
                        orderlines[i].set_line_user(selectedUser);
                    }
                }
            }
        }
    }
    SalespersonButton.template = 'SalespersonButton';
    ProductScreen.addControlButton({
        component: SalespersonButton,
        condition: function() {
            return this.env.pos.config.allow_salesperson;;
        },
    });
    Registries.Component.add(SalespersonButton);
    return SalespersonButton;
});
