INSERT INTO TRANSACTIONS VALUES  (11004,10042,'2023-03-21','ONTIME');
SELECT * FROM EVALUATE_RESULT;
ALTER TABLE EVALUATE_RESULT 
ADD GUIDE_NO VARCHAR(25);
UPDATE EVALUATE_RESULT SET GUIDE_NO = '1201' WHERE USN = '1RV20IS045';
INSERT INTO PHASE_ALLOT VALUES ('10061','1006','1');
DELETE FROM FILE_SUB WHERE SUB_ID = '10061';
DELETE FROM FILE_SUB WHERE SUB_ID = '10061';
INSERT INTO EVALUATE_RESULT VALUES(10042,'1RV20IS045',10,4,4,'');
INSERT INTO EVALUATE_RESULT VALUES (10042,'1RV20IS045',10,4,4,'1201');
DELETE FROM EVALUATE_RESULT WHERE SUB_ID = '10061';