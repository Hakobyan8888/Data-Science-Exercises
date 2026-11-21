import fs from 'node:fs/promises';
import { createRequire } from 'node:module';
const { Workbook } = createRequire(import.meta.url)('@oai/artifact-tool');

// Synthetic practice data. A fixed seed makes reruns reproducible.
let seed = 42;
function randomInteger(min, max) {
  seed = (Math.imul(1664525, seed) + 1013904223) >>> 0;
  return min + Math.floor((seed / 4294967296) * (max - min + 1));
}

const grades = [['Student', 'Math', 'Physics', 'CS']];
for (let i = 1; i <= 20; i++) {
  grades.push([`S${String(i).padStart(2, '0')}`,
    randomInteger(0, 20), randomInteger(0, 20), randomInteger(0, 20)]);
}

const sales = [['Month', 'Electronics_EUR', 'Clothing_EUR', 'Food_EUR', 'Home_EUR']];
const seasonality = [0.85, 0.8, 0.95, 1, 1.05, 1.1, 1.05, 1, 1.05, 1.1, 1.3, 1.5];
for (let i = 0; i < 12; i++) {
  sales.push([`2025-${String(i + 1).padStart(2, '0')}`,
    ...[22000, 16000, 25000, 14000].map(base =>
      Math.round(base * seasonality[i] + randomInteger(-2000, 2000)))]);
}

const survey = [['Preferred_category', 'Respondent']];
const categories = ['Electronics', 'Clothing', 'Food', 'Home'];
for (let i = 1; i <= 30; i++) {
  survey.push([categories[randomInteger(0, 3)], `R${String(i).padStart(2, '0')}`]);
}

const datasets = [
  ['student_grades.csv', 'Grades', grades],
  ['monthly_sales.csv', 'Sales', sales],
  ['survey_responses.csv', 'Survey', survey],
];
const workbook = Workbook.create();
for (const [, name, rows] of datasets) {
  const sheet = workbook.worksheets.add(name);
  sheet.getRangeByIndexes(0, 0, rows.length, rows[0].length).values = rows;
}
workbook.recalculate();
await fs.mkdir('data', { recursive: true });
function csvField(value) {
  const text = String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}
for (const [filename, name, expected] of datasets) {
  const sheet = workbook.worksheets.getItem(name);
  const values = sheet.getRangeByIndexes(0, 0, expected.length, expected[0].length).values;
  if (JSON.stringify(values) !== JSON.stringify(expected)) {
    throw new Error(`Value verification failed: ${filename}`);
  }
  const csv = values.map(row => row.map(csvField).join(',')).join('\r\n') + '\r\n';
  await fs.writeFile(`data/${filename}`, csv, 'utf8');
  console.log(`Created data/${filename}: ${values.length - 1} records`);
}
