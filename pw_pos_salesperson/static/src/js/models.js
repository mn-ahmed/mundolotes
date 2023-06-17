odoo.define('pos_salesperson.models', function(require){
    'use strict';
	var models = require('point_of_sale.models');
	var core = require('web.core');
	var _t = core._t;
    //
    var _super_Orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        init_from_JSON: function (json) {
            var self = this;
            if (json.user_id) {
                var user = this.get_user_by_id(json.user_id);
                if (user) {
                    this.set_line_user(user);
                }
            }
            return _super_Orderline.init_from_JSON.apply(this, arguments);
        },
        //
        export_as_JSON: function () {
            var json = _super_Orderline.export_as_JSON.apply(this, arguments);
            if (this.user_id) {
                json.user_id = this.user_id.id;
            }
            return json;
        },
        //
        get_user_image_url: function () {
            if (this.user_id && this.user_id.id !== undefined) {
                return window.location.origin + '/web/image?model=res.users&field=image_128&id=' + this.user_id.id;
            }
            return null;
        },
        //
        get_user_by_id: function (user_id) {
            var self = this;
            var user = null;
            for (var i = 0; i < self.pos.users.length; i++) {
                if (self.pos.users[i].id == user_id) {
                    user = self.pos.users[i];
                }
            }
            return user;
        },
        //
        get_line_user: function () {
            if (this.user_id && this.user_id.id !== undefined) {
                return this.user_id;
            }
            return null;
        },
        //
        set_line_user: function (user) {
            this.user_id = user;
            this.trigger('change', this);
        },
        //
        remove_sale_person: function () {
            this.user_id = null;
            this.trigger('change', this);
        },
    });
});
