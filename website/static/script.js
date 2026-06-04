// Слайдер
class Slider {
    constructor(container) {
        this.container = container;
        this.slides = container.querySelectorAll('.slide');
        this.prevBtn = container.querySelector('.prev');
        this.nextBtn = container.querySelector('.next');
        this.dotsContainer = container.querySelector('.slider-dots');
        this.currentIndex = 0;
        this.interval = null;
        
        if (this.slides.length > 0) {
            this.createDots();
            this.updateSlides();
            this.startAutoPlay();
            
            if (this.prevBtn) this.prevBtn.addEventListener('click', () => this.prev());
            if (this.nextBtn) this.nextBtn.addEventListener('click', () => this.next());
        }
    }
    //создаёт точки навигаторы
    createDots() {
        if (!this.dotsContainer) return;
        this.dotsContainer.innerHTML = '';
        this.slides.forEach((_, i) => {
            const dot = document.createElement('div');
            dot.classList.add('dot');
            if (i === this.currentIndex) dot.classList.add('active');
            dot.addEventListener('click', () => this.goTo(i));
            this.dotsContainer.appendChild(dot);
        });
    }
    //обновляет изображение и точки
    updateSlides() {
        this.slides.forEach((slide, i) => {
            if (i === this.currentIndex) {
                slide.classList.add('active');
            } else {
                slide.classList.remove('active');
            }
        });
        
        if (this.dotsContainer) {
            const dots = this.dotsContainer.querySelectorAll('.dot');
            dots.forEach((dot, i) => {
                if (i === this.currentIndex) {
                    dot.classList.add('active');
                } else {
                    dot.classList.remove('active');
                }
            });
        }
    }
    //следущий
    next() {
        this.currentIndex = (this.currentIndex + 1) % this.slides.length;
        this.updateSlides();
        this.resetAutoPlay();
    }
    //предыдущий
    prev() {
        this.currentIndex = (this.currentIndex - 1 + this.slides.length) % this.slides.length;
        this.updateSlides();
        this.resetAutoPlay();
    }
    //к определеному
    goTo(index) {
        this.currentIndex = index;
        this.updateSlides();
        this.resetAutoPlay();
    }
    //автоматич переключение
    startAutoPlay() {
        this.interval = setInterval(() => this.next(), 3000);
    }
    //сброс тайиера при ручном переключении
    resetAutoPlay() {
        if (this.interval) {
            clearInterval(this.interval);
            this.startAutoPlay();
        }
    }
}

//инициализация всех слайдеров на странице
document.querySelectorAll('.slider-container').forEach(container => {
    new Slider(container);
});

//валидация форм
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const inputs = this.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                showFieldError(input, 'Это поле обязательно');
            } else if (input.type === 'email' && input.value) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(input.value)) {
                    isValid = false;
                    showFieldError(input, 'Введите корректный email');
                }
            }
        });
        
        if (!isValid) {
            e.preventDefault();
        }
    });
});
// показывает ошибку пере полем ввода
function showFieldError(input, message) {
    const formGroup = input.closest('.form-group');
    if (formGroup) {
        let errorDiv = formGroup.querySelector('.error-message');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            formGroup.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
        input.classList.add('error');
        
        input.addEventListener('input', function() {
            errorDiv.remove();
            input.classList.remove('error');
        }, { once: true });
    }
}

//анимация при загрузке
document.addEventListener('DOMContentLoaded', () => {
    document.body.classList.add('loaded');
});

//плавный скролл
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});