from machine import Pin, PWM


class DCMotor:
    def __init__(self, pin1, pin2, min_duty=300, max_duty=1023, frequency=1023):
        # self.pin1 = PWM(Pin(pin1), frequency)
        # self.pin2 = PWM(Pin(pin2), frequency)
        self.min_duty = min_duty
        self.max_duty = max_duty

    def forward(self, speed):
        # self.pin1.duty(self.duty_cycle(speed))
        # self.pin2.duty(0)
        print("向前")
        pass

    def backward(self, speed):
        # self.pin1.duty(0)
        # self.pin2.duty(self.duty_cycle(speed))
        print(f"向后：{speed}")
        pass

    def stop(self):
        # self.pin1.duty(0)
        # self.pin2.duty(0)
        print("stop")
        pass

    def duty_cycle(self, speed):
        if speed < 0:
            speed = 0
        if speed > 100:
            speed = 100
        duty = int(self.min_duty + (self.max_duty - self.min_duty) * speed / 100.)
        return duty