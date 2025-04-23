document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const htmlElement = document.documentElement;
    
    const savedTheme = getCookie('theme');
    if (savedTheme === 'dark') {
        enableDarkMode();
    } else if (savedTheme === 'light') {
        enableLightMode();
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        enableDarkMode();
    }
    
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            if (htmlElement.getAttribute('data-theme') === 'dark') {
                enableLightMode();
            } else {
                enableDarkMode();
            }
        });
    }
    
    function enableDarkMode() {
        htmlElement.setAttribute('data-theme', 'dark');
        if (darkModeToggle) {
            darkModeToggle.classList.add('active');
        }
        setCookie('theme', 'dark', 365);
    }
    
    function enableLightMode() {
        htmlElement.removeAttribute('data-theme');
        if (darkModeToggle) {
            darkModeToggle.classList.remove('active');
        }
        setCookie('theme', 'light', 365);
    }
    
    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    }
    
    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for(let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }
    
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.nav');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            nav.classList.toggle('active');
            console.log('Menu toggled:', nav.classList.contains('active')); // Debug log
        });
    }
    
    const osButtons = document.querySelectorAll('.os-btn');
    
    function hideAllInstructions(instructionsId) {
        const instructionsContainer = document.getElementById(instructionsId);
        if (instructionsContainer) {
            instructionsContainer.querySelectorAll('.os-instruction').forEach(instruction => {
                instruction.classList.remove('active');
            });
        }
    }
    
    osButtons.forEach(button => {
        button.addEventListener('click', function() {
            const os = this.getAttribute('data-os');
            let instructionsId, targetId;
            
            if (os.includes('-py')) {
                instructionsId = 'python-instructions';
                targetId = 'python-' + os;
            } else {
                instructionsId = 'git-instructions';
                targetId = 'git-' + os;
            }
            
            this.closest('.os-buttons').querySelectorAll('.os-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            this.classList.add('active');
            
            const instructionsContainer = document.getElementById(instructionsId);
            if (instructionsContainer) {
                if (instructionsContainer.style.display === 'block') {
                    if (document.getElementById(targetId).classList.contains('active')) {
                        instructionsContainer.style.display = 'none';
                        this.classList.remove('active');
                        return;
                    }
                } else {
                    instructionsContainer.style.display = 'block';
                }
                
                hideAllInstructions(instructionsId);
                
                const instructionElement = document.getElementById(targetId);
                if (instructionElement) {
                    setTimeout(() => {
                        instructionElement.classList.add('active');
                    }, 50);
                }
            }
        });
    });
    
    const copyButtons = document.querySelectorAll('.copy-btn');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-clipboard-text');
            
            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalIcon = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i>';
                
                setTimeout(() => {
                    this.innerHTML = originalIcon;
                }, 2000);
            }).catch(err => {
                console.error('Could not copy text: ', err);
            });
        });
    });
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                if (nav.classList.contains('active')) {
                    nav.classList.remove('active');
                }
                
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    const highlightCode = () => {
        const codeElement = document.getElementById('source-code');
        if (codeElement) {
            const content = codeElement.textContent;
            
            const keywords = ['import', 'from', 'def', 'async', 'await', 'try', 'except', 'if', 'else', 'return', 'for', 'in', 'not'];
            
            let highlightedContent = content;
            
            keywords.forEach(keyword => {
                const regex = new RegExp(`\\b${keyword}\\b`, 'g');
                highlightedContent = highlightedContent.replace(regex, `<span class="keyword">${keyword}</span>`);
            });
            
            highlightedContent = highlightedContent.replace(/(["'])(?:(?=(\\?))\2.)*?\1/g, '<span class="string">$&</span>');
            
            highlightedContent = highlightedContent.replace(/(#.*$)/gm, '<span class="comment">$1</span>');
            
            codeElement.innerHTML = highlightedContent;
        }
    };
    
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.feature-card, .step, .source-container, .cta-content');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (elementPosition < screenPosition) {
                element.classList.add('animated');
            }
        });
    };
    
    const style = document.createElement('style');
    style.textContent = `
        .os-instructions {
            transition: max-height 0.5s cubic-bezier(0.4, 0, 0.2, 1), 
                        opacity 0.3s ease, 
                        padding 0.3s ease;
        }
        
        .fade-in {
            animation: fadeInContent 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        }
        
        @keyframes fadeInContent {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .feature-card, .step, .source-container, .cta-content {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.6s ease-out, transform 0.6s ease-out;
        }
        
        .feature-card.animated, .step.animated, .source-container.animated, .cta-content.animated {
            opacity: 1;
            transform: translateY(0);
        }
        
        .step:nth-child(2) { transition-delay: 0.1s; }
        .step:nth-child(3) { transition-delay: 0.2s; }
        .step:nth-child(4) { transition-delay: 0.3s; }
        .step:nth-child(5) { transition-delay: 0.4s; }
        .step:nth-child(6) { transition-delay: 0.5s; }
        
        .feature-card:nth-child(2) { transition-delay: 0.1s; }
        .feature-card:nth-child(3) { transition-delay: 0.2s; }
        .feature-card:nth-child(4) { transition-delay: 0.3s; }
        
        /* Code syntax highlighting colors */
        .keyword { color: #ff79c6; }
        .string { color: #f1fa8c; }
        .comment { color: #6272a4; }
    `;
    document.head.appendChild(style);
    
    highlightCode();
    animateOnScroll();
    
    window.addEventListener('scroll', animateOnScroll);
});
