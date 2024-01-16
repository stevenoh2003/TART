import {ShoppingCartProvider} from "../contextShoppingCartContext"

function HigherLevel(){
    return (
        <ShoppingCartProvider>
            {SubmitButton}
        </ShoppingCartProvider>
    );
}