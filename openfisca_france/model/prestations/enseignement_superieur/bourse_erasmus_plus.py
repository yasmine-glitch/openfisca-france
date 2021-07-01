from numpy import timedelta64
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import YEAR, MONTH
from openfisca_core.variables import Variable

from openfisca_france.entities import Individu


class bourse_erasmus_plus_stage_montant(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant"
    documentation = '''
        Conditions non modélisées :
        La variation du montant de la bourse selon la destination et le type de mobilité
        '''
    def formula(individu, period, parameters):
        bourse_erasmus_plus_stage_eligibilite = individu('bourse_erasmus_plus_stage_eligibilite', period)
        bourse_erasmus_plus_stage_montant = parameters(period).prestations.erasmus_plus.montant_stage
        return bourse_erasmus_plus_stage_eligibilite * bourse_erasmus_plus_stage_montant



class bourse_erasmus_plus_stage_eligibilite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    default_value = False
    label = "Eligibilité pour la bourse Erasmus+ de type stage"
    documentation = '''
        Conditions non modélisées :
        La possibilité de bénéficier d'1 an de mobilité pour études et/ou stages Erasmus + par cycle d'études (licence, master, doctorat).
        La possibilité de bénéficier de l'aide dans certains états non membres de l'UE : République de Macédoine du Nord, la Serbie, l'Islande, le Liechtenstein, la Norvège, la Turquie.
        '''

    def formula(individu, period, parameters):
        debut_etudes_etranger = individu('debut_etudes_etranger', period)
        fin_etudes_etranger = individu('fin_etudes_etranger', period)
        etudiant_pays_eee = individu('pays_etudes_eee', period)
        bourse_criteres_sociaux_eligibilite = individu('bourse_criteres_sociaux_eligibilite', period)
        duree_etudes_etranger = (fin_etudes_etranger - debut_etudes_etranger).astype('timedelta64[M]')

        eligibilite_duree_min = duree_etudes_etranger >= timedelta64(parameters(period).prestations.erasmus_plus.duree.mois_min, 'M')
        eligibilite_duree_max = duree_etudes_etranger <= timedelta64(parameters(period).prestations.erasmus_plus.duree.mois_max, 'M')

        return etudiant_pays_eee * bourse_criteres_sociaux_eligibilite * eligibilite_duree_min * eligibilite_duree_max