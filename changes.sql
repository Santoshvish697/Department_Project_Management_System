UPDATE DELIVERABLE_PROJECT SET Project_Title = "Medical Chatbot" WHERE Project_ID = 1005;

UPDATE GUIDE SET USN = '1RV20IS045' WHERE GUIDE_ID = '1201';
UPDATE GUIDE SET USN = '1RV20IS043' WHERE GUIDE_ID = '1204';
UPDATE GUIDE SET USN = '1RV20IS036' WHERE GUIDE_ID = '1203';
UPDATE GUIDE SET USN = '1RV20IS006' WHERE GUIDE_ID = '1202';

CREATE TABLE PANEL_ALLOT (
ALLOT_NUM INTEGER PRIMARY KEY AUTO_INCREMENT,
GUIDE_ID VARCHAR(25),
PANEL_ID INTEGER,
FOREIGN KEY (GUIDE_ID) REFERENCES GUIDE(GUIDE_ID),
FOREIGN KEY (PANEL_ID) REFERENCES PANEL_MEMBERS(PANEL_ID)
);

INSERT INTO PANEL_ALLOT (Guide_ID,Panel_ID) VALUES ('1201',100), ('1202',104), ('1203',102), ('1204',103);

CREATE TABLE PHASE_ALLOT (
phase_ID INTEGER PRIMARY KEY auto_increment,
Project_ID INTEGER,
phase_no INTEGER,
due_date DATE,
FOREIGN KEY (Project_ID) REFERENCES DELIVERABLE_PROJECT(Project_ID)
);

INSERT INTO PHASE_ALLOT VALUES (1203,1003,1,20222-09-03);
INSERT INTO PHASE_ALLOT VALUES (1204,1004,1,20222-10-04);
INSERT INTO PHASE_ALLOT VALUES (1205,1005,0,20222-10-23);
INSERT INTO PHASE_ALLOT VALUES (1206,1006,0,20222-09-03);

SELECT * FROM PHASE_ALLOT;

UPDATE PHASE_ALLOT SET Phase_ID = 1303 WHERE Phase_ID = 1203;
UPDATE PHASE_ALLOT SET Phase_ID = 1304 WHERE Phase_ID = 1204;

UPDATE PHASE_ALLOT SET LATE_SUBMISSION = "LATE" WHERE PHASE_ID = 1301;
UPDATE PHASE_ALLOT SET LATE_SUBMISSION = "LATE" WHERE PHASE_ID = 1302;

---Update as of 01-02-2023