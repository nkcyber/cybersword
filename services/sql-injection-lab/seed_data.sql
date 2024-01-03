DROP TABLE IF EXISTS notes;
CREATE TABLE IF NOT EXISTS notes (
    name TEXT,
    securityCode TEXT,
    content TEXT
);

-- include flag insertions first so they're returned first
-- TODO: derive from flags with python script
INSERT INTO documents VALUES("FLAG #1", "SuperDuperSecret", "FLAG_1");
INSERT INTO notes VALUES("FLAG #2", "SuperSecretNote", "FLAG_2");
INSERT INTO documents VALUES("Mac & Cheese Ingredients", "General", "Ingredient for Mac & Cheese: Mac, Cheese");
INSERT INTO documents VALUES("Mac & Cheese Instructions", "General", "Combine Mac with Cheese");
INSERT INTO documents VALUES("Attack Plans", "SuperDuperSecret", "We attack at dawn. Be there or be square.");
INSERT INTO documents VALUES("Welcome!", "", "This document has an empty security code");

INSERT INTO documents VALUES("Marketing Plan", "Confidential", "This document outlines the company's marketing strategy.");
INSERT INTO documents VALUES("Research Paper", "General", "This paper presents the findings of a recent research study.");
INSERT INTO documents VALUES("Technical Manual", "Internal", "This manual provides instructions for using a specific product or system.");
INSERT INTO documents VALUES("Press Release", "Public", "This release announces a company news to the public.");

INSERT INTO notes VALUES("Research Proposal", "Confidential", "This proposal was written by Dr. Jane Smith.");
INSERT INTO notes VALUES("Marketing Report", "Internal", "This report was prepared by the Marketing Team.");
INSERT INTO notes VALUES("Meeting Agenda", "General", "This agenda was created by the meeting organizer.");
INSERT INTO notes VALUES("Project Status Update", "Internal", "This update was written by the Project Manager.");
