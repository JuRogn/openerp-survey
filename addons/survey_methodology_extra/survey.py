# -*- coding: utf-8 -*-
##############################################################################
#
#    Survey Methodology
#    Copyright (C) 2013 Coop. Trab. Moldeo Interactive Ltda.
#    No email
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import re
import netsvc
from osv import osv, fields
import random
import itertools

class survey(osv.osv):
    """"""
    _name = 'survey_methodology.survey'
    _inherit = [ _name ]

    def generate_sample(self, cr, uid, ids, context=None):
        """"""
        context = context or {}
        partner_obj = self.pool.get('res.partner')

        for survey in self.browse(cr, uid, ids, context):
            sample_size = survey.sample_size
            sample_filter = survey.sample_filter and eval(survey.sample_filter) or []
            respondent_ids = partner_obj.search(cr, uid, [('is_respondent','=',True)] + sample_filter)
            sample_ids = random.sample(respondent_ids, sample_size)
            self.write(cr, uid, survey.id, {'respondent_ids': [(6,0,sample_ids)] })

        return True

    def generate_questions(self, cr, uid, ids, context=None):
        """
        Create root answer for this survey.
        """
        context = context or {}
        partner_obj = self.pool.get('res.partner')
        user_obj = self.pool.get('res.partner')
        question_obj = self.pool.get('survey_methodology.question')
        questionnaire_obj = self.pool.get('survey_methodology.questionnaire')
        answer_obj = self.pool.get('survey_methodology.answer')
        q_ids = []

        for survey in self.browse(cr, uid, ids, context):
            survey_id = survey.id
            respondent_ids = context.get('respondent_ids', [ p.id for p in survey.respondent_ids ])
            for respondent_id in respondent_ids:
                q_ids = questionnaire_obj.search(cr, uid, [
                    ('respondent_id','=',respondent_id),
                    ('survey_id','=',survey_id)
                ])
                if q_ids:
                    continue

                v = {
                    'name': survey.name,
                    'respondent_id': respondent_id,
                    'pollster_id': context.get('pollster_id', False),
                    'survey_id': survey_id,
                }
                q_ids.append(questionnaire_obj.create(cr, uid, v));

        return q_ids

survey()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
