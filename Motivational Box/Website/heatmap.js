// Read the data from db.json
fetch('db.json')
    .then(response => response.json())
    .then(data => {
        const heatmapContainer = document.getElementById('heatmap-container');

        // Get the earliest date from the data
        const dates = Object.keys(data);
        const earliestDate = new Date(Math.min(...dates.map(date => new Date(date))));

        // Get the current date
        const currentDate = new Date();

        // Generate the heatmap
        for (let date = earliestDate; date <= currentDate.setFullYear(currentDate.getFullYear() + 1); date.setDate(date.getDate() + 1)) {
            const dateString = formatDate(date);
            const tasks = data[dateString] || {};

            const dayElement = document.createElement('div');
            dayElement.className = 'day';

            const dateElement = document.createElement('div');
            dateElement.className = 'date';
            dateElement.textContent = formatDateDisplay(date);
            dayElement.appendChild(dateElement);

            if (date > currentDate) {
                dayElement.classList.add('future');
            } else {
                const taskContainer = document.createElement('div');
                taskContainer.className = 'task-container';

                Object.entries(tasks).forEach(([task, completed]) => {
                    const taskWrapperElement = document.createElement('div');
                    const taskElement = document.createElement('div');
                    const taskNameElement = document.createElement('div');

                    taskWrapperElement.className = 'task-wrapper';
                    taskElement.className = completed ? 'completed' : 'incomplete';
                    taskNameElement.className = 'task-name';

                    taskNameElement.textContent = task;
                    taskElement.appendChild(taskNameElement);
                    taskWrapperElement.appendChild(taskElement);
                    taskContainer.appendChild(taskWrapperElement);
                });

                dayElement.appendChild(taskContainer);
            }

            heatmapContainer.appendChild(dayElement);
        }
    });

// Format the date as "YYYY/M/D" for consistency
function formatDate(date) {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    return `${year}/${month}/${day}`;
}

// Format the date as "M/D" for display
function formatDateDisplay(date) {
    const month = date.getMonth() + 1;
    const day = date.getDate();
    return `${month}/${day}`;
}