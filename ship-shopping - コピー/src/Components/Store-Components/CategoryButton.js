import React from "react";
import { Button } from "react-bootstrap";

export function CategoryButton({ categories = [], setSelectedCategory }) {
  return (
    <>
      {categories.map(category => (
        <Button key={category} onClick={() => setSelectedCategory(category)}>
          {category}
        </Button>
      ))}
    </>
  );
}
