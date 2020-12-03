const express = require('express'),
	app = express(),
	bodyParser = require('body-parser');


const spacesRoutes = require('./routes/spaces.js');
const indexRoutes = require('./routes/index.js');

const port = 5000;

app.use(express.json());


app.use("/spaces", spacesRoutes);

app.use("/", indexRoutes);

app.listen(port, "localhost", () => {
	console.log(`App started on port: ${port}`);
})