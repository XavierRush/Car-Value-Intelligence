const express = require('express');
const nunjucks = require('nunjucks');
const path = require('path');
const fs = require('fs');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const START_PORT = Number(process.env.PORT || 3000);
const baseDir = __dirname;
const templatesDir = path.join(baseDir, 'templates');
const staticDir = path.join(baseDir, 'static');
const dbDir = path.join(baseDir, 'database');
const dbPath = path.join(dbDir, 'cars.db');

if (!fs.existsSync(dbDir)) {
	fs.mkdirSync(dbDir, { recursive: true });
}

const depreciationRates = {
	sedan: 0.10,
	suv: 0.08,
	truck: 0.07,
	luxury: 0.15,
};

const insuranceBase = {
	sedan: 1200,
	suv: 1400,
	truck: 1300,
	luxury: 2000,
};

const db = new sqlite3.Database(dbPath);

const nunjucksEnv = nunjucks.configure(templatesDir, {
	autoescape: true,
	express: app,
});

nunjucksEnv.addGlobal('url_for', (endpoint, options = {}) => {
	if (endpoint === 'static' && options.filename) {
		return `/static/${options.filename}`;
	}
	return '/';
});

nunjucksEnv.addFilter('currency', (value) => formatCurrency(value));

app.use(express.urlencoded({ extended: true }));
app.use('/static', express.static(staticDir));

function round(value, digits = 2) {
	return Number.parseFloat(Number(value).toFixed(digits));
}

function formatCurrency(value) {
	return new Intl.NumberFormat('en-US', {
		minimumFractionDigits: 0,
		maximumFractionDigits: 0,
	}).format(Number(value || 0));
}

function estimateValue(price, age, mileage, vehicleType) {
	const rate = depreciationRates[vehicleType] ?? 0.10;
	let value = Number(price);

	for (let index = 0; index < Number(age); index += 1) {
		value *= 1 - rate;
	}

	value -= Number(mileage) * 0.05;

	return round(Math.max(value, 0));
}

function estimateCosts(milesPerYear, vehicleType, age) {
	let insuranceCost = insuranceBase[vehicleType] ?? 1500;

	if (age !== null && age > 5) {
		insuranceCost *= 0.85;
	}

	const fuelCost = Number(milesPerYear) * 0.12;
	const maintenanceCost = Number(milesPerYear) * 0.05;
	const registrationCost = 150;
	const totalAnnual = fuelCost + maintenanceCost + insuranceCost + registrationCost;

	return {
		fuel: round(fuelCost),
		maintenance: round(maintenanceCost),
		insurance: round(insuranceCost),
		registration: registrationCost,
		total_annual: round(totalAnnual),
		cost_per_month: round(totalAnnual / 12),
	};
}

function getRecommendation(age, mileage) {
	if (age > 10 || mileage > 150000) {
		return {
			action: 'Sell the car at this value.',
			reasoning:
				'This car is older or has high mileage, so depreciation is likely already cutting into its value. Selling now can help you avoid extra repair costs and lock in a reasonable return.',
		};
	}

	if (age < 5 && mileage < 60000) {
		return {
			action: 'Hold on to the car for now.',
			reasoning:
				'This car is still fairly young and has relatively low mileage. If the market stays healthy, waiting a bit longer may let you get more money in the end.',
		};
	}

	return {
		action: 'Watch the market closely.',
		reasoning:
			'The car is in a middle ground. It may be worth holding for a little while, but a drop in value or rising repair costs could make selling sooner the smarter move.',
	};
}

function buildNarrative(make, model, age, mileage, price, value) {
	const retention = price > 0 ? Math.round((value / price) * 100) : 0;
	return `${make} ${model} is estimated to retain about ${retention}% of its original value after ${age} years and ${mileage.toLocaleString()} miles.`;
}

function createTableIfNeeded() {
	db.serialize(() => {
		db.run(`
			CREATE TABLE IF NOT EXISTS valuations(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				make TEXT,
				model TEXT,
				vehicle_type TEXT,
				price REAL,
				age INTEGER,
				mileage INTEGER,
				estimated_value REAL,
				created_at TEXT DEFAULT CURRENT_TIMESTAMP
			)
		`);
	});
}

function saveValuation(row) {
	const createdAt = new Date().toISOString();
	db.run(
		`
			INSERT INTO valuations (
				make, model, vehicle_type, price, age, mileage, estimated_value, created_at
			) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
		`,
		[
			row.make,
			row.model,
			row.vehicle_type,
			row.price,
			row.age,
			row.mileage,
			row.estimated_value,
			createdAt,
		],
	);
}

function getRecentValuations(limit = 5) {
	return new Promise((resolve, reject) => {
		db.all(
			`
				SELECT make, model, vehicle_type, price, age, mileage, estimated_value, created_at
				FROM valuations
				ORDER BY id DESC
				LIMIT ?
			`,
			[limit],
			(error, rows) => {
				if (error) {
					reject(error);
					return;
				}

				resolve(rows || []);
			},
		);
	});
}

app.get('/', (request, response) => {
	response.render('landingpage.html');
});

app.get('/evaluate', (request, response) => {
	response.render('index.html', { result: null });
});

app.post('/calculate', async (request, response, next) => {
	try {
		const make = request.body.make || '';
		const model = request.body.model || '';
		const price = Number(request.body.price || 0);
		const age = Number(request.body.age || 0);
		const mileage = Number(request.body.mileage || 0);
		const vehicleType = request.body.vehicle_type || 'sedan';

		const estimatedValue = estimateValue(price, age, mileage, vehicleType);
		const costs = estimateCosts(12000, vehicleType, age);
		const recommendation = getRecommendation(age, mileage);
		const narrative = buildNarrative(make, model, age, mileage, price, estimatedValue);

		saveValuation({
			make,
			model,
			vehicle_type: vehicleType,
			price,
			age,
			mileage,
			estimated_value: estimatedValue,
		});

		const recentQueries = await getRecentValuations(5);
		const retainPct = price > 0 ? Math.max(Math.round((estimatedValue / price) * 100), 0) : 0;
		const result = {
			make,
			model,
			vehicle_type: vehicleType,
			price,
			age,
			mileage,
			estimated: estimatedValue,
			age_loss: round(price - price * Math.pow(1 - (depreciationRates[vehicleType] ?? 0.1), age)),
			mile_loss: round(mileage * 0.05),
			retain_pct: retainPct,
		};

		response.render('results.html', {
			value: formatCurrency(estimatedValue),
			recommendation,
			narrative,
			recent_queries: recentQueries.map((item) => ({
				...item,
				estimated_value: formatCurrency(item.estimated_value),
			})),
			costs,
			result,
		});
	} catch (error) {
		next(error);
	}
});

app.get('/history', async (request, response, next) => {
	try {
		const queries = await getRecentValuations(20);
		response.render('history.html', { queries });
	} catch (error) {
		next(error);
	}
});

app.use((error, request, response, next) => {
	console.error(error);
	response.status(500).send('Server error');
});

createTableIfNeeded();

function startServer(port) {
	const server = app.listen(port, () => {
		console.log(`Server running at http://127.0.0.1:${port}`);
	});

	server.on('error', (error) => {
		if (error.code === 'EADDRINUSE') {
			console.log(`Port ${port} is in use, trying ${port + 1}...`);
			startServer(port + 1);
			return;
		}

		throw error;
	});
}

startServer(START_PORT);
