const express = require('express');
const fs = require('fs');
require('dotenv').config()

const app = express();

app.use(express.static(__dirname + '/public'));
app.set('view engine', 'ejs');
app.set('views', './views');

let rawdata = fs.readFileSync(__dirname + '/data/data.json');
const data = JSON.parse(rawdata);

let categoryData = {};
for (let book of data) {
    splited = book.author.split('Visite a página de ')
    if (splited.length > 1)
        book.author = splited[1]
    for (let category of book.categories) {
        if (!(category in categoryData))
            categoryData[category] = [book];
        else
            categoryData[category].push(book);
    }
}

const PORT = process.env.PORT || 80;

app.get('/', (req, res) => {
    if (req.query.search) {
        let search = req.query.search;
        let results = [];
        for (let book of data) {
            let title = book.title;
            if (title.toLowerCase().match(`^.*${search.toLowerCase()}.*$`))
                results.push(book);
        }
        res.render('search.ejs', {results: results});
    }
    else
        res.render('index.ejs', {categories: categoryData});
})

app.get('/:title', (req, res) => {
    let desiredBook = null;
    for (let book of data) {
        if (book.title === req.params.title)
            desiredBook = book;
    }
    if (desiredBook === null)
        res.render('notfound.ejs');
    else
        res.render('book.ejs', desiredBook);
})

app.listen(PORT, () => {
    console.log(`Server listening on http://localhost:${PORT}`);
});