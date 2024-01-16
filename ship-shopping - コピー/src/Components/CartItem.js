
import { useShoppingCart } from "../context/ShoppingCartContext";
import data from "../data/items.json";
import group from "../data/recipe.json";
import { Button, Stack } from "react-bootstrap";
import { formatCurrency } from "../utilities/formatCurrency";
import React, { useState, useEffect, useContext } from "react";
import { ShoppingCartContext } from "../context/ShoppingCartContext";


export function CartItem({id, quantity}) {
    const { removeFromCart, selectedItem, setSelectedItem} = useContext(ShoppingCartContext);

    const item = data.find(i => i.id === id);
    const recipeitem = group.find(j => j.id === id);

    const [ingredientIds, setIngredientIds] = useState([]);


    useEffect(() => {
        if (item) {
            setSelectedItem(prevItems => {
                const isItemExist = prevItems.some(prevItem => prevItem.id === item.id);
                if (!isItemExist) {
                    return [...prevItems, item];
                }
                return prevItems;
            });
        }
    }, [item,setSelectedItem]);

    useEffect(() => {
        if (recipeitem) {
            let ids;
            switch (recipeitem.name){
                case "Curry":
                    ids = [5, 10, 13];
                    break;
                case "Blueberry Pie":
                    ids = [14, 15, 16];
                    break;
                case "Hamburger":
                    ids = [6, 10, 11];
                    break;
                case "Salad":
                    ids = [11, 12];
                    break;
                default:
                    ids = [];
            }
            setIngredientIds(ids);
        } 
    }, [recipeitem]);


    const [ingredientItems, setIngredientItems] = useState([]);
    useEffect(() => {
        const items = ingredientIds.map(id => data.find(i => i.id === id));
        setIngredientItems(items);
    }, [ingredientIds]);


    const renderIngredients = () => {
        return ingredientItems.map((ingredient, index) => {

            //console.log("ingredient", ingredient);
            
            return (
                <Stack key={index} direction="horizontal" gap={2} className="d-flex align-items-center">
                    <img src={ingredient.imgUrl} style={{ width: "125px", height: "75px", objectFit: "cover" }} />
                    <div>
                        {ingredient.name}{quantity > 1 && <span className="text-muted" style={{ fontSize: "0.65rem" }}>x{quantity}</span>}
                    </div>
                    <div className="text-muted" style={{ fontSize: "0.75rem" }}>
                        {formatCurrency(ingredient.price)}
                    </div>
                    <div>
                        {formatCurrency(ingredient.price * quantity)}
                        <Button variant="outline-danger" size="sm" onClick={() => removeFromCart(ingredient.id)}>×</Button>
                    </div>
                </Stack>     
            );
        })
    };

    


    const renderContent= () => {
        if (item != null) {
            //console.log("item", item);
            return (
                <Stack direction="horizontal" gap={2} className="d-flex align-items-center">
                    <img src={item.imgUrl} style={{ width: "125px", height: "75px", objectFit: "cover" }} />
                    <div>
                        <div>
                            {item.name}{quantity > 1 && <span className="text-muted" style={{ fontSize: "0.65rem" }}>x{quantity}</span>}
                        </div>
                        <div className="text-muted" style={{ fontSize: "0.75rem" }}>
                            {formatCurrency(item.price)}
                        </div>
                    </div>
                    <div>
                        {formatCurrency(item.price * quantity)}
                        <Button variant="outline-danger" size="sm" onClick={() => removeFromCart(item.id)}>×</Button>
                    </div>
                </Stack>
            );
        } else if (recipeitem != null) {
            return renderIngredients();
        } else {
            return null;
        }
    };
    
    
    // console.log("item: ", item);
    // console.log("id", id);
    // console.log("ingredientItem", ingredientItems);
    // console.log("ingredientIds", ingredientIds);
    


    return(
        
            <div>
                {renderContent()}
            </div>
        
    );
}

