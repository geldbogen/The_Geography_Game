window.myNamespace = Object.assign({}, window.myNamespace, {  
    mySubNamespace: {  
        my_style: function(feature, context) {  
            const player_color_dict = context.hideout.player_color_dict;
            const country_owner_dict = context.hideout.country_owner_dict;
            const selected = context.hideout.selected;
            const country_name = feature.properties.sovereignt;
            var ans = {};
            if(selected.includes(country_name)){
                ans['className'] = 'pulsing-country';
            }

            if(Object.keys(country_owner_dict).includes(country_name)){
                const country_owner = country_owner_dict[country_name];
                if (country_owner == 'Nobody') {
                    ans['fillColor'] = 'grey';
                    ans['color'] = 'grey';
                }
                ans['fillColor'] = player_color_dict[country_owner];
                ans['color'] = 'grey';
            }
            return ans;
        },
    }
});