import { useShoppingCart } from "../context/ShoppingCartContext";
import group from "../data/recipe.json";
import { Button, Stack } from "react-bootstrap";
import { formatCurrency } from "../utilities/formatCurrency";

export function CartRecipe({ uniqueID, quantity }) {
    const { removeFromCart } = useShoppingCart();
    const recipeitem = group.find(j => j.uniqueID === uniqueID);

    if (recipeitem == null) return null;

    return (
        <div>
            <Stack direction="horizontal" gap={2} className="d-flex align-items-center">
                <img src={recipeitem.imgUrl} style={{ width: "125px", height: "75px", objectFit: "cover" }} />
                <div>
                    <div>
                        {recipeitem.name}{quantity > 1 && <span className="text-muted" style={{ fontSize: "0.65rem" }}>x{quantity}</span>}
                    </div>
                    <div className="text-muted" style={{ fontSize: "0.75rem" }}>
                        {formatCurrency(recipeitem.price)}
                    </div>
                </div>
                <div>
                    {formatCurrency(recipeitem.price * quantity)}
                    <Button variant="outline-danger" size="sm" onClick={() => removeFromCart(recipeitem.uniqueID)}>×</Button>
                </div>
            </Stack>
        </div>      
    );
}
