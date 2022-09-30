///** @odoo-module **/
//
//const patchMixin = require("web.patchMixin");
//const PatchableMessage = patchMixin(components.activity_mark_done_popover);
////const activity_mark_done_popover = require(".js");
//import { ActivityMarkDonePopover } from "@mail/src/activity_mark_done_popover";
//
//PatchableMessage.patch(
//    "tata_location_based_activity/static/src/tata_activity_geolocation.js",
//    (T) => {
//        class MessagePatched extends T {
//            /**
//             * @override property
//              */
//        async _onClickDone() {
//
//alert("sdfsj")
//}        }
//        return MessagePatched;
//    }
//);
//ActivityMarkDonePopover.components.ActivityMarkDonePopover  = PatchableMessage;