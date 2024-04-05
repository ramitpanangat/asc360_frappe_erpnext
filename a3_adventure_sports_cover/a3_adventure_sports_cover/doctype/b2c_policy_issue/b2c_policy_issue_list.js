frappe.listview_settings['B2C Policy Issue'] = {

    onload(listview) {
         // triggers once before the list is loaded
         listview.page.add_action_item('Download Document', () => {
            var items = Object();
            var count = 0;
            // make a array of all checked items in listview
            listview.get_checked_items(true).map(e => {
                items[count] = e;
                count += 1
            })
            frappe.call({
                // calling a python function to get lis of all download links
                method: "a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2c_policy_issue.events.download_pdf",
                args: items,
                callback: function(r){
                    // dynamically create hidden <a> tag for all links and click it automatically to download pdf
                    for(var index=0; index <= Object.keys(r.message).length; index++){
                        console.log(r.message[index])
                        var link = document.createElement('a');
                        link.href = r.message[index];
                        link.download = r.message[index].substr(r.message[index].lastIndexOf('/') + 1);
                        link.click();
                    }
                    
                }
            })
         });
        
   }
 }