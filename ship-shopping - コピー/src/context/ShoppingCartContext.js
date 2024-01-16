/*
import { createContext, useContext, useState } from "react";
import { ShoppingCart } from "../Components/ShoppingCart";

const ShoppingCartContext = createContext({});

export function useShoppingCart() {
  return useContext(ShoppingCartContext);
}

export function ShoppingCartProvider({ children }) {
  const [isOpen, setIsOpen] = useState(false);
  const [cartItems, setCartItems] = useState([]);

  const cartQuantity = cartItems.reduce((quantity, item) => item.quantity + quantity, 0);

  const openCart = () => setIsOpen(true);
  const closeCart = () => setIsOpen(false);

  function getItemQuantity(id) {
    return cartItems.find((item) => item.id === id)?.quantity || 0;
  }

  function increaseCartQuantity(id) {
    setCartItems((currItems) => {
      if (currItems.find((item) => item.id === id) == null) {
        return [...currItems, { id, quantity: 1 }];
      } else {
        return currItems.map((item) => {
          if (item.id === id) {
            return { ...item, quantity: item.quantity + 1 };
          } else {
            return item;
          }
        });
      }
    });
  }

  function decreaseCartQuantity(id) {
    setCartItems((currItems) => {
      const currentItem = currItems.find((item) => item.id === id);
      if (currentItem && currentItem.quantity === 1) {
        return currItems.filter((item) => item.id !== id);
      } else {
        return currItems.map((item) => {
          if (item.id === id) {
            return { ...item, quantity: item.quantity - 1 };
          } else {
            return item;
          }
        });
      }
    });
  }

  
  function removeFromCart(id) {
    setCartItems((currItems) => currItems.filter((item) => item.id !== id));
  }
  

  return (
    <ShoppingCartContext.Provider
      value={{ 
        getItemQuantity, 
        increaseCartQuantity, 
        decreaseCartQuantity, 
        removeFromCart,
        openCart, 
        closeCart,
        cartItems,
        cartQuantity
      }}
    >
      {children}
      <ShoppingCart isOpen={isOpen} />
    </ShoppingCartContext.Provider>
  );
}
*/


import { createContext, useContext, useState } from "react";
import { ShoppingCart } from "../Components/ShoppingCart";


export const ShoppingCartContext = createContext();

export function useShoppingCart(){
  return useContext(ShoppingCartContext);
}

export function ShoppingCartProvider({ children }) {
  //const [cartItems, setCartItems] = useState([]);
  const [selectedItem, setSelectedItem] = useState([]);
  
  const [isOpen, setIsOpen] = useState(false);
  const [cartItems, setCartItems] = useState([]);

  const cartQuantity = cartItems.reduce((quantity, item) => item.quantity + quantity, 0);

  const openCart = () => setIsOpen(true);
  const closeCart = () => setIsOpen(false);

  function getItemQuantity(id) {
    return cartItems.find((item) => item.id === id || item.ingredientIds === id)?.quantity || 0;
  }

  //console.log("item in the cart", cartItems );
  
  function increaseCartQuantity(id) {
    setCartItems((currItems) => {
      if (currItems.find((item) => item.id === id) == null) {
        return [...currItems, { id, quantity: 1 }];
      } else {
        return currItems.map((item) => {
          if (item.id === id) {
            return { ...item, quantity: item.quantity + 1 };
          } else {
            return item;
          }
        });
      }
    });
  } 
  

  
  // function increaseCartQuantity(id, isIngredient = false) {
  //   setCartItems((currItems) => {
  //     const identifier = id > 16 ? 'ingredientIds' : 'id';
  //     console.log("Identifier used: ", identifier);
  //     console.log("id", id);
  //     let itemInCart = currItems.find((item) => item[identifier] === id);

  //     if (!itemInCart) {
  //       const newItem = isIngredient ? {ingredientIds : id, quantity: 1} : {id, quantity: 1};
  //       return [...currItems, newItem];
  //     } else {
  //       return currItems.map((item) => {
  //         if (item[identifier] === id) {
  //           return { ...item, quantity: item.quantity + 1 };
  //         } else {
  //           return item;
  //         }
  //       });
  //     }
  //   });
  // }
  

  // function increaseCartQuantity(id, ingredientIds){
  //   let itemInCart = currItems.find((item) => item[identifier] === id);
  //   if (id > 16){
  //     setCartItems((currItems) => {
  //       let itemInCart = currItems.find((item) => item.ingredientIds === id);
  //     })
  //     if (!itemInCart) {
  //       const newItem = {ingredientIds : id, quantity: 1};
  //       return [...currItems, newItem];
  //     } else {
  //       return currItems.map((item) => {
  //         if (item.ingredientIds === id) {
  //           return { ...item, quantity: item.quantity + 1};
  //         } else {
  //           return item;
  //         }
  //       });
  //     }
  //   } else {
  //     setCartItems((currItems) => {
  //       let itemInCart = currItems.find((item) => item.id === id);
  //     })
  //     if (!itemInCart) {
  //       const newItem = {id : id, quantity: 1};
  //       return [...currItems, newItem];
  //     } else {
  //       return currItems.map((item) => {
  //         if (item.id === id) {
  //           return { ...item, quantity: item.quantity + 1};
  //         } else {
  //           return item;
  //         }
  //       });
  //     }
  //   }
  // }
  

  // function increaseCartQuantity(id, ingredientIds) {
  //   setCartItems(currItems => {
  //     let newItems = [...currItems];
  //     console.log("id", id)
  //     console.log("ingredientIds", ingredientIds)
  
  //     if (id > 16) {
  //       // Check if id is an array. If not, treat it as an array with a single element
  //       const ingredientIds = Array.isArray(id) ? id : [id];
  //       //console.log("ingredientIds", ingredientIds);
  
  //       ingredientIds.forEach(ingredientId => {
  //         const itemInCart = newItems.find(item => item.ingredientIds && item.ingredientIds.includes(ingredientId));
  //         if (!itemInCart) {
  //           newItems.push({ ingredientIds: [ingredientId], quantity: 1 });
  //         } else {
  //           newItems = newItems.map(item => {
  //             if (item.ingredientIds && item.ingredientIds.includes(ingredientId)) {
  //               return { ...item, quantity: item.quantity + 1 };
  //             } else {
  //               return item;
  //             }
  //           });
  //         }
  //       });
  //     } else {
  //       // Single item update
  //       const itemInCart = newItems.find(item => item.id === id);
  //       if (!itemInCart) {
  //         newItems.push({ id: id, quantity: 1 });
  //       } else {
  //         newItems = newItems.map(item => {
  //           if (item.id === id) {
  //             return { ...item, quantity: item.quantity + 1 };
  //           } else {
  //             return item;
  //           }
  //         });
  //       }
  //     }
  
  //     return newItems;
  //   });
  // }
  

  
  


  function decreaseCartQuantity(id, isIngredient = false) {
    setCartItems((currItems) => {
      const identifier = isIngredient ? 'ingredientIds' : 'id';
      const currentItem = currItems.find((item) => item[identifier] === id);
      if (currentItem && currentItem.quantity === 1) {
        return currItems.filter((item) => item[identifier] !== id);
      } else {
        return currItems.map((item) => {
          if (item[identifier] === id) {
            return { ...item, quantity: item.quantity - 1 };
          } else {
            return item;
          }
        });
      }
    });
  }


  function removeFromCart(id, ingredientIds) {
    const ingredientIdsArray = Array.isArray(ingredientIds) ? ingredientIds : [ingredientIds];
    //console.log("ids", {id, ingredientIds});

    setCartItems(currItems => currItems.filter(item => {
      if (item.id === id) return false;

      if (item.ingredientIds && ingredientIdsArray.some(ingId => item.ingredientIds.include(ingId))){
        return false;
      }
      return true;
    }));
  }
  
  /*
  function removeFromCart(id) {
    console.log("Removing item from cart", { id });
    setCartItems(currItems => {
      return currItems.reduce((newCartItems, item) => {
        if (item.ingredientIds && item.ingredientIds.includes(id)){
          const updatedIngredientIds = item.ingredientIds.filter(ingredientId => ingredientId !== id);
          if (updatedIngredientIds.length > 0){
            newCartItems.push({...item, ingredientIds: updatedIngredientIds});
            
          }
        } else {
          newCartItems.push(item);
        }
        return newCartItems;
      }, []);
    });
  }
  */

  
  
  

  return (
    <ShoppingCartContext.Provider
      value={{ 
        cartItems,
        setCartItems,
        selectedItem,
        setSelectedItem,
        isOpen,
        setIsOpen,

        getItemQuantity, 
        increaseCartQuantity, 
        decreaseCartQuantity, 
        removeFromCart,
        openCart, 
        closeCart,
        cartItems,
        cartQuantity
      }}
    >
      {children}
      <ShoppingCart isOpen={isOpen} />
    </ShoppingCartContext.Provider>
  );
}