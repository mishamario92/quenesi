package {
    import flash.display.Sprite;
    import flash.events.Event;

    // Имя класса должно совпадать с именем файла Main.as
    public class Main extends Sprite {
        
        // Создаем переменную для нашего квадрата
        private var myBox:Sprite;

        // Это главная функция (конструктор), она запускается сама при старте
        public function Main() {
            trace("Программа на AS3 успешно запущена!");
            
            createSquare(); // Рисуем квадрат
            startAnimation(); // Запускаем движение
        }

        // Функция рисует синий квадрат прямо из кода
        private function createSquare():void {
            myBox = new Sprite();
            myBox.graphics.beginFill(0x0000FF); // Синий цвет
            myBox.graphics.drawRect(0, 0, 50, 50); // Размеры 50х50 пикселей
            myBox.graphics.endFill();
            
            addChild(myBox); // Добавляем квадрат на экран
        }

        // Функция включает постоянное обновление экрана
        private function startAnimation():void {
            addEventListener(Event.ENTER_FRAME, onLoop);
        }

        // Этот код работает каждый кадр и двигает квадрат
        private function onLoop(e:Event):void {
            myBox.x += 3; // Двигаем вправо
            
            // Если ушел за экран (640 пикселей), возвращаем назад
            if (myBox.x > 640) {
                myBox.x = -50;
            }
        }
    }
}
