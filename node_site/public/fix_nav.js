const fs = require('fs');
const path = require('path');

const directoryPath = __dirname;

fs.readdir(directoryPath, (err, files) => {
    if (err) {
        return console.log('Unable to scan directory: ' + err);
    }
    files.forEach(file => {
        if (file.endsWith('.html')) {
            let filePath = path.join(directoryPath, file);
            let content = fs.readFileSync(filePath, 'utf8');
            
            let updated = content.replace(/>COURSES<\/a>/g, '>Courses</a>');
            updated = updated.replace(/>COLLABORATE<\/a>/g, '>Collaborate</a>');
            
            if (content !== updated) {
                fs.writeFileSync(filePath, updated);
                console.log(`Updated ${file}`);
            }
        }
    });
});
