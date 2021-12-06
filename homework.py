"""Программа для работы фитнес-трекера."""


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Сообщение о тренировке."""
        info_message = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.'
                        )
        return info_message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dist_in_km = self.action * self.LEN_STEP / self.M_IN_KM
        return dist_in_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_spead = self.get_distance() / self.duration
        return mean_spead

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        information = InfoMessage(type(self).__name__,
                                  self.duration,
                                  self.get_distance(),
                                  self.get_mean_speed(),
                                  self.get_spent_calories()
                                  )
        return information


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_cal_1: int = 18
        coeff_cal_2: int = 20
        dur_in_min: float = self.duration * 60
        calories: float = ((coeff_cal_1 * self.get_mean_speed() - coeff_cal_2)
                           * self.weight / self.M_IN_KM * dur_in_min)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_cal_1: float = 0.035
        coeff_cal_2: float = 0.029
        dur_in_min: float = self.duration * 60
        calories: float = ((coeff_cal_1 * self.weight
                           + (self.get_mean_speed()**2 // self.height)
                           * coeff_cal_2 * self.weight) * dur_in_min)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_spead = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_spead

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_cal_1: float = 1.1
        coeff_cal_2: float = 2
        calories: float = ((self.get_mean_speed() + coeff_cal_1)
                           * coeff_cal_2 * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    conform_dict = {'SWM': Swimming,
       'RUN': Running,
       'WLK': SportsWalking,
        }
    object_: Training = conform_dict[workout_type](*data)
    return object_


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type_, data_ in packages:
        training_ = read_package(workout_type_, data_)
        main(training_)
