import pandas as pd
import numpy as np
import sympy as sym

from .interpolation_methods import Interpolation_Methods

class Interpolation:

    def __int__(self, data: pd.DataFrame, percentage : float):

        df_missing = data.copy()
        df_missing.y = self.delete(df_missing.y.copy(), percentage)

        self.obj_interpolar = Interpolation_Methods(df_missing.y)

        return self._generate_data()

    def delete(self, column, percentage):

        n = np.floor(len(column)*percentage)
        i = np.floor(len(column)/n)
        index = 1
        for _ in range(int(n)):
            pos = np.random.randint(2,int(i)+1)
            index += pos
            column.iloc[index] = np.nan

        return column

    def cut_interval(self, interval, y_interval, min_pol):

        first_interval = interval[:min_pol+1]
        first_interval_y = y_interval[:min_pol+1]
        second_interval = []
        second_interval_y = []

        done = False
        for i, x in enumerate(interval[min_pol+1:]):
            if x != first_interval[-1] + 1 and not done:
                first_interval.append(x)
                first_interval_y.append(y_interval[i])
            else:
                second_interval.append(x)
                second_interval_y.append(y_interval[i])
                done = True

        return first_interval, second_interval, first_interval_y, second_interval_y

    def get_intervals(self, min_pol, max_pol):

        # Auxiliaries
        interval = []
        intervals = []
        y_interval = []
        y_intervals = []

        y = self.obj_interpolar.y

        for i, x in enumerate(self.obj_interpolar.xx):

            # if i == 55 or i == 56 or i == 57:
            #     print(x)
            #     print(interval)
            #     print(intervals)

            # Llenar la lista hasta su maximo
            if len(interval) == max_pol or i == len(self.obj_interpolar.xx)-1:

                if i == len(self.obj_interpolar.xx)-1:
                    if interval == []:
                        interval = intervals[-1]
                        interval.append(x)
                        intervals[-1] = interval

                        y_interval = y_intervals[-1]
                        y_interval.append(y[i])
                        y_intervals = y_interval

                    else:
                        interval.append(x)
                        intervals.append(interval)

                        y_interval.append(y[i])
                        y_intervals.append(y_interval)
                else:
                    intervals.append(interval) 
                    interval = [x]

                    y_intervals.append(y_interval)
                    y_interval = [y[i]]

            elif len(interval)+1 >= min_pol:
                if self.obj_interpolar.xx[i+1] == x+1:
                    interval.append(x)
                    intervals.append(interval)
                    interval = []

                    y_interval.append(y[i])
                    y_intervals.append(y_interval)
                    y_interval = []
                else:
                    interval.append(x)
                    y_interval.append(y[i])
            # Si el intervalo esta vacio
            elif interval == []:

                # Verificar si lista de intervalos esta vacia
                if intervals != []:


                    if x != intervals[-1][-1] + 1:
                        first_interval, second_interval, first_interval_y, second_interval_y = self.cut_interval(intervals[-1], y_intervals[-1], min_pol)
                        intervals[-1] = first_interval
                        y_intervals[-1] = first_interval_y
                        interval = second_interval
                        y_interval = second_interval_y

                        if len(interval) < max_pol:
                            interval.append(x)
                            y_interval.append(y[i])
                        else:
                            intervals.append(interval)
                            y_intervals.append(y_interval)
                            interval = [x]
                            y_interval = [y[i]]

                    # Se puede agregar con tranquilidad, no hay discontinuidades
                    else:
                        interval.append(x)
                        y_interval.append(y[i])
                # Si esta vacia simplemente adicione elementos al intervalo actual
                # ya que esta construyendo el primer interbalo
                else:
                    interval.append(x)
                    y_interval.append(y[i])
            
            # Si no esta vacio y no ha alzanzado el maximo adicionar hasta llegar a su 
            # maximo
            else:
                interval.append(x)
                y_interval.append(y[i])

        interval_tuples = [(interval[0], interval[-1]) for interval in intervals]

        return interval_tuples, intervals, y_intervals

    def correct_intervals(self, interval_tuples):

        last = -1
        malos = 0
        algo_pasa = []

        aux_inter_tuples = []

        for i, inter in enumerate(interval_tuples):

            print(inter)

            if last != inter[0]-1:
                print('ALGO PASA')
                aux_inter_tuples.append((last,inter[0]))
                algo_pasa.append(i)
                malos +=1

            aux_inter_tuples.append(inter)

            last = inter[1]

        print(malos)
        print(algo_pasa)

        return aux_inter_tuples

    def interpolate_intervals(self, intervals):

        x_interpolate = []
        y_interpolate = []

        l=sym.Symbol('x')
        cont = 0
        for inter in intervals:
            # print(inter)
            beg = self.obj_interpolar.xx.index(inter[0])
            end = self.obj_interpolar.xx.index(inter[1])

            datos_interpolar_x = self.obj_interpolar.xx[beg:end+1]
            datos_interpolar_y = self.obj_interpolar.y[beg:end+1]
            funcion = self.obj_interpolar.lagrange_interpolation(datos_interpolar_x,datos_interpolar_y)

            for x in np.arange(datos_interpolar_x[0],datos_interpolar_x[-1]+1, 1):
                # print(x)
                cont += 1
                x_interpolate.append(x)
                y = funcion.subs(l,x)
                y_interpolate.append(y)

        # print(cont)

        return x_interpolate, y_interpolate

    def _generate_data(self):

        interval_tuples, intervals, y_intervals = self.get_intervals(3,6)
        aux_inter_tuples = self.correct_intervals(interval_tuples)

        x_interpolate, y_interpolate = self.interpolate_intervals(aux_inter_tuples)

        ds = [self.data.ds.iloc[x] for x in x_interpolate]

        df_interpolate = pd.DataFrame({'ds':ds, 'y':y_interpolate})
        df_interpolate = df_interpolate.drop_duplicates(subset = 'ds', keep = 'first').reset_index(drop = True)

        return df_interpolate