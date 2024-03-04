import { useShoppingCart } from "../context/ShoppingCartContext";
import data from "../data/items.json";
import { Button, Stack } from "react-bootstrap";
import { formatCurrency } from "../utilities/formatCurrency";

export function CartFood({ id, quantity }) {
    const { removeFromCart } = useShoppingCart();
    const item = data.find(i => i.id === id);

    if (item == null) return null;

    return (
        <div>
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
        </div>      
    );
}
