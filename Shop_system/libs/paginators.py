# 函数作用是为了返回一个页面范围的生成器 <Page m of n>
def page_range_func(paginator, current_page, max_pages):
    # 当前数据量过多导致页面数大于允许的最大页面数
    if paginator.num_pages > max_pages:
        if current_page - max_pages//2 < 1:
            page_range_data = range(1,max_pages)
        elif current_page + max_pages//2 > paginator.num_pages:
            page_range_data = range(current_page - max_pages//2, paginator.num_pages + 1)
        else:
            page_range_data = range(current_page - max_pages//2, current_page + max_pages//2)
    else:
        page_range_data = paginator.page_range
    '''
    @property
    def page_range(self):
        """
        Returns a 1-based range of pages for iterating through within
        a template for loop.
        """
        return six.moves.range(1, self.num_pages + 1)
    '''
    return page_range_data


