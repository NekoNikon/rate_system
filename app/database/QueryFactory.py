class QF():
    def select_all(self):
        return '''
                SELECT
                    *
                FROM
                    select_all
                '''


    def add_user_in_manage_persons(self , log , pswd , prvg):
        return '''
            INSERT INTO
                manage_persons(
                    manage_persons_login ,
                    manage_persons_password ,
                    manage_persons_priv_value
                )
                VALUES (
                    '%s' ,
                    '%s' ,
                    '%s'
                )
        ''' % (log , pswd , prvg)

    def add_rate(self ,ids,idi,idt,val):
        return '''
        DO
        $do$
        BEGIN
        IF EXISTS 
                    (SELECT * FROM rate WHERE rate_indicator_id=%(idi)i and rate_teacher_id=%(idt)i and rate_season_id= %(ids)i )
                THEN
                UPDATE 
                    rate SET rate_value = %(val)f
                    WHERE 
                        rate_indicator_id=%(idi)i and rate_teacher_id=%(idt)i and rate_season_id= %(ids)i ;
                ELSE 
                    INSERT INTO 
                        rate(rate_value , rate_teacher_id , rate_indicator_id , rate_season_id) 
                        VALUES ('%(val)f' , '%(idt)i' , '%(idi)i' , '%(ids)i') ;
        END IF;
        END
        $do$
        ''' % {'val':val , 'idt':idt , 'idi':idi , 'ids':ids}

    # TODO fix query get_teacher_rate_by_iin() add condition for date
    def get_teacher_rate_by_iin(self,iin):
        # rate.rate_teacher_id ,
        #                 teachers.teachers_second_name  ,teachers.teachers_first_name ,
        #                 season.season_date ,
        #                 indicator.indicator_name ,
        return '''SELECT
                        indicator.indicator_name ,
                        rate.rate_value,
                        season.season_date
                     FROM
                        rate ,
                        teachers ,
                        season ,
                        indicator ,
                        indicator_group
                    WHERE
                        teachers.teachers_iin='{0:s}'
                    AND
                        rate.rate_season_id=season.season_id
                    AND
                        rate.rate_teacher_id = teachers.teachers_id
                    AND
                        rate.rate_indicator_id = indicator.indicator_id
                    AND
                        indicator.indicator_group_id = indicator_group.indicator_group_id ORDER BY season_date DESC'''.format(iin)

    def get_teachers_and_rate_value_by_manager_teachers(self , id_mp  ,id_season):
    	return '''
    			SELECT *
                FROM teachers , teachers_group , manage_persons
                WHERE
                    manage_persons.manage_persons_id=1
                    AND
                    teachers.teachers_id = teachers_group.teachers_group_teacher_id
                    AND
                    manage_persons.manage_persons_id=teachers_group.teachers_group_head_teachers_id
    			''' % (id_mp , id_season)
