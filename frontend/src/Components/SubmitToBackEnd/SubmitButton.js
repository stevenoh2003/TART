// import { Button } from "react-bootstrap";
// import {CartItem} from "../CartItem"
// import {ShowAll} from "../CartItem"
// import React, { useContext } from 'react';

// export function SubmitButton(id){
//     function handleSubmit(){
//         console.log("id:", id);
//     }

//     return (
//         <Button onClick={handleSubmit}>Submit</Button>
//     );
// }

import React, {useContext} from "react";
import {ShoppingCartContext} from "../../context/ShoppingCartContext";
import { Button } from "react-bootstrap";


export function SubmitButton(){
    const {selectedItems, selectedItem} = useContext(ShoppingCartContext);

    // const downloadJson = () => {
    //     const jsonStr = JSON.stringify(selectedItems, null, 2);
    //     const blob = new Blob([jsonStr], {type: "application/json"});
    //     const url = URL.createObjectURL(blob);
    //     const link = document.createElement("a");
    //     link.href = url;
    //     link.download = "selectedItems.json";
    //     link.click();
    // };

    function handleSubmit(){
        console.log("selectedItem", selectedItem);
    }

    return(
        <div>
            {/* {selectedItem && <p>Selected Item: {selectedItem.name}</p>} */}
            <Button onClick={handleSubmit}>Submit</Button>
            {/* <Button onClock={downloadJson}>Download JSON</Button> */}
        </div>
    );
}