   	const tabs = document.querySelectorAll('.tab-link');
        const tabContents = document.querySelectorAll('.tab-content');

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                
                tabs.forEach(t => t.classList.remove('active'));
                tabContents.forEach(c => c.classList.remove('active'));

                
                tab.classList.add('active');
                const targetTabContent = document.getElementById(tab.dataset.tab);
                targetTabContent.classList.add('active');
            });
        });