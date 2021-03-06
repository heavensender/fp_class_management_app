#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '1.0.0.0'


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CustomPaginator(Paginator):
    
    def __init__(self, current_page, per_pager_num, *agrs, **kwargs):
        
        self.current_page = int(current_page)
        self.per_pager_num = int(per_pager_num)
        super(CustomPaginator, self).__init__(*agrs, **kwargs)


    def pager_num_range(self):
        
        if self.num_pages < self.per_pager_num:
            return range(1, self.num_pages+1)

        half_part = int(self.per_pager_num/2)  
        if self.current_page <= half_part:
            return range(1, self.per_pager_num+1)
        else:
            if (self.current_page+half_part) > self.num_pages:
                return range(self.num_pages-self.per_pager_num+1, self.num_pages+1)
            else:
                return range(self.current_page-half_part, self.current_page+half_part)
