frappe.listview_settings['B2B Policy Issue'] = {

    onload(listview) {
         // triggers once before the list is loaded
         $('a.grey-link').each(function() {
            var data = $(this).text()
            if(data.includes("Cancel")){
            $(this).remove();
            }
        });
        listview.page.add_action_item('Cancel',()=>{
            var cancel_item = Object();
            var cancel_count = 0;
            listview.get_checked_items(true).map(e => {
                cancel_item[cancel_count] = e;
                cancel_count += 1
            })
            frappe.call({
                method: "a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2b_policy_issue.events.cancel_checked",
                args: cancel_item,
                callback: function(r){
                    console.log(r.message)
                }
            })
        })
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
                method: "a3_adventure_sports_cover.a3_adventure_sports_cover.doctype.b2b_policy_issue.events.download_pdf",
                args: items,
                callback: async function(r){
                    // dynamically create hidden <a> tag for all links and click it automatically to download pdf
                    for(var index=0; index <= Object.keys(r.message).length; index++){
                        var link = document.createElement('a');
                        link.href = r.message[index];
                        link.download = r.message[index].substr(r.message[index].lastIndexOf('/') + 1);
                        link.click();
                        await new Promise(r => setTimeout(r, 1000));
                    }
                    
                }
            })
         });
        
   }
 }