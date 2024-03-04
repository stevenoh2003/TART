import React from "react";
import { SearchingBar } from "../Components/Store-Components/SearchingBar";
import Data from "../data/items.json";
import { ItemStore } from "../Components/Store-Components/ItemStore";
import { Col, Row, Button } from "react-bootstrap";
import { useState } from "react";
import { CategoryButton } from "../Components/Store-Components/CategoryButton";

export function Store() {
  const [query, setQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const categories = [...new Set(Data.map(item => item.category))];
  const filteredData = Data.filter((item) => {
    const queryMatch = item.name.toLowerCase().includes(query.toLowerCase());
    const categoryMatch = selectedCategory === "All" || item.category === selectedCategory;
    return queryMatch && categoryMatch;
  });

  const clearInput = () => {
    setSelectedCategory("All");
    setQuery("");
  };

  return (
    <div>
      <h1>Store</h1>

      <div className="mb-3">
        <SearchingBar query={query} setQuery={setQuery} />
      </div>

      <div className="mb-3">
        <CategoryButton categories={categories} setSelectedCategory={setSelectedCategory} />
      </div>

      <div>
        <Button onClick={clearInput}>Clear</Button>
      </div>

      <Row md={2} xs={1} lg={3} className="g-3">
        {filteredData.map((item, index) => (
          <Col key={index}>
            <ItemStore {...item} />
          </Col>
        ))}
      </Row>
    </div>
  );
}
