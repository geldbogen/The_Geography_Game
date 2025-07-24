window.myNamespace = Object.assign({}, window.myNamespace, {  
    mySubNamespace: {  
        my_style: function(feature, context) {  
            const player_color_dict = context.hideout.player_color_dict;
            const country_owner_dict = context.hideout.country_owner_dict;
            const country_name = feature.properties.name;

            if(Object.keys(country_owner_dict).includes(country_name)){
                const country_owner = country_owner_dict[country_name];
                return {fillColor: player_color_dict[country_owner], color: 'grey'}
            }
            return {fillColor: 'grey', color: 'grey'}  
        },
        doubleclick: function(e, ctx) {
                console.log(`You double-clicked at ${e.latlng}.`);
            }
    }
});