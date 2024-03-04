import group from "../data/recipe.json";
import { RecipeStore } from "../Components/Recipe-Components/RecipeStore";
import { Col, Row} from "react-bootstrap";

export function Recipe() {
    return (
        <div>
            <h1>Recipe</h1>

            <Row md={2} xs={1} lg={3} className="g-3">
                {group.map((item, index) => (
                    <Col key={index}>
                        <RecipeStore {...item} />
                    </Col>
                ))}
            </Row>
        </div>
    );
}
