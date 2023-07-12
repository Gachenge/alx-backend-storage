-- create a trigger that reduces quantity after adding a new order
-- quantity can be negative
CREATE TRIGGER reduce AFTER INSERT ON orders
	FOR EACH ROW UPDATE items SET quantity = quantity - NEW.number WHERE name = NEW.item_name;
