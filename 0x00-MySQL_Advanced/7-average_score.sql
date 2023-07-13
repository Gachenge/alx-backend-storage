-- script that creates a stored procedure ComputeAverageScoreForUser that computes the average score for a tudent
-- average score can be a decimal
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(
	IN suser_id INT)
BEGIN
	DECLARE avg_score FLOAT DEFAULT 0;
	SET avg_score = (SELECT AVG(score) FROM corrections WHERE user_id=suser_id);
	UPDATE users SET average_score=avg_score WHERE id = suser_id;
END $$
DELIMITER ;
