window.myNamespace = Object.assign({}, window.myNamespace, {  
    mySubNamespace: {  
        my_style: function(feature, context) {  
            const {selected} = context.hideout;
            if(selected.includes(feature.properties.name)){
                return {fillColor: 'red', color: 'grey'}
            }
            return {fillColor: 'grey', color: 'grey'}  
        },
        doubleclick: function(e, ctx) {
                console.log(`You double-clicked at ${e.latlng}.`);
            }
    }
});